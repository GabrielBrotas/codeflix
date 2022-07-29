import { CategoryRepository } from "../../../domain/category/repository/category.repository";
import { CategoryOutput, CategoryOutputMapper } from "../../dto/category-output";
import {default as DefaultUseCase} from "../../use-case";
import { SearchInputDto } from "../../../domain/@seedwork/dto/search-input";
import {
  PaginationOutputDto,
  PaginationOutputMapper,
} from "../../../domain/@seedwork/dto/pagination-output";

export namespace ListCategoriesUseCase {
  export class UseCase implements DefaultUseCase<Input, Output> {
    constructor(private categoryRepo: CategoryRepository.Repository) {}
    //
    async execute(input: Input): Promise<Output> {
      const params = new CategoryRepository.SearchParams(input);
      const searchResult = await this.categoryRepo.search(params);
      return this.toOutput(searchResult);
    }
  
    private toOutput(searchResult: CategoryRepository.SearchResult): Output {
      const items = searchResult.items.map((i) => {
        return CategoryOutputMapper.toOutput(i);
      });
      return PaginationOutputMapper.toOutput(items, searchResult);
    }
  }

  export type Input = SearchInputDto;

  export type Output = PaginationOutputDto<CategoryOutput>;
  
}

export default ListCategoriesUseCase;

//request e response http
//dados - Category - dados de saida

//UseCase -> domain

//infra -> domain
